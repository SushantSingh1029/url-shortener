import { useEffect, useState } from 'react';
import api from '../api/axios';

const Dashboard = () => {
    const [analytics, setAnalytics] = useState({
        total_urls: 0,
        total_clicks: 0,
        most_clicked_url: '-'
    });

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                const response = await api.get('/users/me/analytics');
                setAnalytics(response.data);
            } catch (error) {
                console.error("Failed to fetch analytics", error);
            }
        };
        fetchAnalytics();
    }, []);

    return (
        <div className="p-6 max-w-7xl mx-auto">
            <h1 className="text-2xl font-semibold text-gray-900 mb-6">Dashboard Overview</h1>
            
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <dt className="text-sm font-medium text-gray-500 truncate">Total URLs</dt>
                        <dd className="mt-1 text-3xl font-semibold text-gray-900">{analytics.total_urls}</dd>
                    </div>
                </div>
                
                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <dt className="text-sm font-medium text-gray-500 truncate">Total Clicks</dt>
                        <dd className="mt-1 text-3xl font-semibold text-gray-900">{analytics.total_clicks}</dd>
                    </div>
                </div>
                
                <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <dt className="text-sm font-medium text-gray-500 truncate">Most Clicked</dt>
                        <dd className="mt-1 text-xl font-semibold text-gray-900 truncate">{analytics.most_clicked_url || '-'}</dd>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;