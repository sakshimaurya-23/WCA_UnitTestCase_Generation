// Frontend code

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [reports, setReports] = useState([]);
    const [search, setSearch] = useState('');
    const [filters, setFilters] = useState({
        customerName: '',
        hospitalName: '',
        wardName: ''
    });

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        try {
            const response = await axios.get('http://localhost:8000/reports/', {
                params: {
                    ...filters,
                    search
                }
            });
            setReports(response.data);
        } catch (error) {
            console.error('Error fetching reports:', error);
        }
    };

    const handleSearch = (e) => {
        setSearch(e.target.value);
        fetchReports();
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters(prevFilters => ({
            ...prevFilters,
            [name]: value
        }));
        fetchReports();
    };

    const handleReset = () => {
        setSearch('');
        setFilters({
            customerName: '',
            hospitalName: '',
            wardName: ''
        });
        fetchReports();
    };

    const handleDownload = async (format) => {
        try {
            const response = await axios.get(`http://localhost:8000/reports/download/${format}`, {
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `reports.${format}`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error(`Error downloading reports in ${format} format:`, error);
        }
    };

    return (
        <div className="app">
            <h1>Reports</h1>
            <div className="search-bar">
                <input
                    type="text"
                    placeholder="Search by keyword"
                    value={search}
                    onChange={handleSearch}
                />
            </div>
            <div className="filters">
                <input
                    type="text"
                    name="customerName"
                    placeholder="Filter by Customer Name"
                    value={filters.customerName}
                    onChange={handleFilterChange}
                />
                <input
                    type="text"
                    name="hospitalName"
                    placeholder="Filter by Hospital Name"
                    value={filters.hospitalName}
                    onChange={handleFilterChange}
                />
                <input
                    type="text"
                    name="wardName"
                    placeholder="Filter by Ward Name"
                    value={filters.wardName}
                    onChange={handleFilterChange}
                />
            </div>
            <button className="reset-button" onClick={handleReset}>Reset</button>
            <table className="report-table">
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Customer Name</th>
                        <th>Hospital Name</th>
                        <th>Ward Name</th>
                        <th>Grade</th>
                        <th>Date</th>
                        <th>Shift Time</th>
                    </tr>
                </thead>
                <tbody>
                    {reports.map(report => (
                        <tr key={report.id}>
                            <td>{report.id}</td>
                            <td>{report.customer_name}</td>
                            <td>{report.hospital_name}</td>
                            <td>{report.ward_name}</td>
                            <td>{report.grade}</td>
                            <td>{report.date}</td>
                            <td>{report.shift_time}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="download-buttons">
                <button onClick={() => handleDownload('csv')}>Download CSV</button>
                <button onClick={() => handleDownload('excel')}>Download Excel</button>
                <button onClick={() => handleDownload('pdf')}>Download PDF</button>
            </div>
        </div>
    );
}

export default App;