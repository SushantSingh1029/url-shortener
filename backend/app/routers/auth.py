from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import (
    Token,
    RefreshTokenRequest,
    ForgotPassword,
    ResetPassword,
)
from app.services.auth_service import (
    register_user,
    create_password_reset_token,
    reset_password,
)
from app.utils.security import verify_password
from app.models.user import User
from app.models.token_blocklist import TokenBlocklist
from app.utils.token import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.dependencies import get_current_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- REGISTER ----------------

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_in)

    # Email verification disabled in deployed demo.
    # Re-enable when SMTP is configured.

    return user


# ---------------- LOGIN ----------------

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# ---------------- REFRESH ----------------

@router.post("/refresh", response_model=Token)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    payload = decode_token(request.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    jti = payload.get("jti")

    if jti and db.query(TokenBlocklist).filter(
        TokenBlocklist.jti == jti
    ).first():
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked",
        )

    user_id = payload.get("sub")

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    new_refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    if jti:
        db.add(TokenBlocklist(jti=jti))
        db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


# ---------------- LOGOUT ----------------

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
    current_token: str = Depends(get_current_token),
):
    access_payload = decode_token(current_token)

    if access_payload and access_payload.get("jti"):
        db.add(
            TokenBlocklist(
                jti=access_payload.get("jti")
            )
        )

    refresh_payload = decode_token(
        request.refresh_token
    )

    if refresh_payload and refresh_payload.get("jti"):
        db.add(
            TokenBlocklist(
                jti=refresh_payload.get("jti")
            )
        )

    db.commit()

    return None


# ---------------- FORGOT PASSWORD ----------------

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPassword,
    db: Session = Depends(get_db),
):
    return {
        "message": "Password reset email is temporarily unavailable in the deployed demo."
    }


# ---------------- RESET PASSWORD ----------------

@router.post("/reset-password")
def reset_password_endpoint(
    request: ResetPassword,
    db: Session = Depends(get_db),
):
    success = reset_password(
        db,
        request.token,
        request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token",
        )

    return {
        "message": "Password has been successfully reset."
    }