import React, { useState } from 'react';
import api from '../api/api';

export const Jobs = () => {
    const [jobDetails, setJobDetails] = useState({
        title: '',
        desc: '',
        employer: '',
        location: '',
        salary: ''
    });
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setJobDetails(prevDetails => ({
            ...prevDetails,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
		setMessage('');
        try {
            const data = await api.postJob(jobDetails);
            setMessage(data.message);

			setJobDetails({
                title: '',
                desc: '',
                employer: '',
                location: '',
                salary: ''
            });
        } catch (error) {
            console.error('Error posting job:', error);
            setMessage('Failed to post job. Please try again.');
        }
    };

    return (
        <div className="page">
            <h2>Post a Job/Internship</h2>
            {message && <p>{message}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title:</label>
                    <input
                        type="text"
                        name="title"
                        value={jobDetails.title}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label>Description:</label>
                    <textarea
                        name="desc"
                        value={jobDetails.desc}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label>Employer:</label>
                    <input
                        type="text"
                        name="employer"
                        value={jobDetails.employer}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label>Location:</label>
                    <input
                        type="text"
                        name="location"
                        value={jobDetails.location}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label>Salary:</label>
                    <input
                        type="text"
                        name="salary"
                        value={jobDetails.salary}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit">Post Job</button>
            </form>
        </div>
    );
};
