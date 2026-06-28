import { useEffect, useState } from 'react';
import api from '../api/axios';

const UrlManagement = () => {
    const [urls, setUrls] = useState([]);
    const [originalUrl, setOriginalUrl] = useState('');
    const [customAlias, setCustomAlias] = useState('');
    const [error, setError] = useState('');

    const fetchUrls = async () => {
        try {
            const response = await api.get('/urls/');
            setUrls(response.data);
        } catch (error) {
            console.error("Failed to fetch URLs", error);
        }
    };

    useEffect(() => {
        fetchUrls();
    }, []);

    const handleCreate = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await api.post('/urls/', {
                original_url: originalUrl,
                custom_alias: customAlias || null
            });
            setOriginalUrl('');
            setCustomAlias('');
            fetchUrls();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create URL');
        }
    };

    const handleDelete = async (id) => {
        try {
            await api.delete(`/urls/${id}`);
            fetchUrls();
        } catch (error) {
            console.error("Failed to delete URL", error);
        }
    };

    const handleCopy = (shortCode) => {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
        const baseUrl = apiUrl.replace(/\/api\/?$/, ''); // Remove /api
        const fullUrl = `${baseUrl}/${shortCode}`;
        navigator.clipboard.writeText(fullUrl);
        alert('Copied to clipboard!');
    };

    return (
        <div className="p-6 max-w-7xl mx-auto">
            <h1 className="text-2xl font-semibold text-gray-900 mb-6">Manage URLs</h1>
            
            <div className="bg-white shadow rounded-lg p-6 mb-8">
                <h2 className="text-lg font-medium mb-4">Create New URL</h2>
                {error && <p className="text-sm text-red-600 mb-4">{error}</p>}
                <form onSubmit={handleCreate} className="flex flex-col sm:flex-row gap-4">
                    <input
                        type="url"
                        placeholder="https://example.com"
                        required
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        value={originalUrl}
                        onChange={(e) => setOriginalUrl(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Custom Alias (optional)"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        value={customAlias}
                        onChange={(e) => setCustomAlias(e.target.value)}
                    />
                    <button
                        type="submit"
                        className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                        Shorten
                    </button>
                </form>
            </div>

            <div className="bg-white shadow rounded-lg overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Original URL</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Short Code</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Clicks</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {urls.map((url) => (
                            <tr key={url.id}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 truncate max-w-xs">{url.original_url}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">{url.short_code}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{url.clicks}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                                    <button onClick={() => handleCopy(url.short_code)} className="text-blue-600 hover:text-blue-900">Copy</button>
                                    <button onClick={() => handleDelete(url.id)} className="text-red-600 hover:text-red-900">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default UrlManagement;
