import React, { useState, useEffect } from 'react';
import api from '../api/api';
import { AuthData } from '../auth/AuthWrapper';
import {
	Menu,
	MenuItem,
	IconButton,
	Accordion,
	AccordionSummary,
	AccordionDetails,
	Typography 
} from '@mui/material'
import MoreVertIcon from '@mui/icons-material/MoreVert';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export const Jobs = () => {
	const { user } = AuthData();
    const [savedJobs, setSavedJobs] = useState([]);
	const [activeTab, setActiveTab] = useState('all'); // 'all', 'my', or 'saved'
    const [anchorEl, setAnchorEl] = useState(null);
    const [selectedJob, setSelectedJob] = useState(null);
    const [message, setMessage] = useState('');
	const [jobs, setJobs] = useState([]);
    const [jobDetails, setJobDetails] = useState({
        title: '',
        desc: '',
        employer: '',
        location: '',
        salary: ''
    });

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
			const fetchedJobs = await api.fetchAllJobs();
			setJobs(fetchedJobs);
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

	const openMenu = (event, job) => {
		event.preventDefault();
		event.stopPropagation();
        setAnchorEl(event.currentTarget);
        setSelectedJob(job);
    };

    const closeMenu = () => {
        setAnchorEl(null);
        setSelectedJob(null);
    };

    const handleTabChange = (tabName) => {
        setActiveTab(tabName);
    };

    const handleSaveUnsaveJob = async (job_id, isSaved) => {
        try {
            if (isSaved) {
                await api.unsaveJob(job_id);
            } else {
                await api.saveJob(job_id);
            }
            // Refresh saved jobs after action
            const fetchedSavedJobs = await api.fetchSavedJobs();
            setSavedJobs(fetchedSavedJobs);
            setMessage(isSaved ? 'Job unsaved successfully.' : 'Job saved successfully.');
        } catch (error) {
            console.error('Error saving/unsaving job:', error);
            setMessage('Failed to update job. Please try again.');
        }
        closeMenu();
    };

	const isJobSaved = (job_id) => {
		return savedJobs.some(savedJob => savedJob.job_id === job_id);
	}

    let displayedJobs = jobs;
    if (activeTab === 'my') {
        displayedJobs = jobs.filter(job => job.owner_user_id === user.user_id);
    } else if (activeTab === 'saved') {
        displayedJobs = savedJobs;
    }

	useEffect(() => {
        const fetchJobs = async () => {
            try {
                const fetchedJobs = await api.fetchAllJobs();
                setJobs(fetchedJobs);
            } catch (error) {
                console.error('Error fetching jobs:', error);
            }
        };

        const fetchSavedJobs = async () => {
            try {
                const fetchedSavedJobs = await api.fetchSavedJobs();
                setSavedJobs(fetchedSavedJobs);
            } catch (error) {
                console.error('Error fetching saved jobs:', error);
            }
        };

        fetchJobs();
        fetchSavedJobs();
    }, []);

	const handleDelete = async (job_id) => {
		try {
			const data = await api.deleteJob(job_id);
			const fetchedJobs = await api.fetchAllJobs();
			setJobs(fetchedJobs);
			setMessage(data.message);
		}
		catch (error) {
			console.error('Error deleting job:', error);
			setMessage('Failed to delete job. Please try again.');
		}
	}

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

			<div className="tabs">
                <button onClick={() => handleTabChange('all')}>All Jobs</button>
                <button onClick={() => handleTabChange('my')}>My Jobs</button>
                <button onClick={() => handleTabChange('saved')}>Saved Jobs</button>
            </div>

			<div className="jobs-list">
				<Typography variant="h6">{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Jobs</Typography>
				{displayedJobs.map((job, index) => (
					<Accordion key={index}>
						<AccordionSummary
							expandIcon={<ExpandMoreIcon />}
							aria-controls={`panel${index}-content`}
							id={`panel${index}-header`}
						>
							<Typography>{job.title}</Typography>
							<IconButton onClick={(event) => openMenu(event, job)} size="small" sx={{ ml: 'auto', mr: -1 }}>
								<MoreVertIcon />
							</IconButton>
						</AccordionSummary>
						<AccordionDetails>
							<Typography>Description: {job.desc}</Typography>
							<Typography>Employer: {job.employer}</Typography>
							<Typography>Location: {job.location}</Typography>
							<Typography>Salary: {job.salary}</Typography>
						</AccordionDetails>
					</Accordion>
				))}
				<Menu
					anchorEl={anchorEl}
					keepMounted
					open={Boolean(anchorEl)}
					onClose={closeMenu}
				>
					{selectedJob && (
						<>
							{activeTab !== 'saved' && (
								<MenuItem onClick={() => handleSaveUnsaveJob(selectedJob.job_id, isJobSaved(selectedJob.job_id))}>
									{isJobSaved(selectedJob.job_id) ? 'Unsave' : 'Save'}
								</MenuItem>
							)}
							{activeTab === 'saved' && (
								<MenuItem onClick={() => handleSaveUnsaveJob(selectedJob.job_id, true)}>Unsave</MenuItem>
							)}
							{activeTab === 'my' && (
								<MenuItem onClick={() => handleDelete(selectedJob.job_id)}>Delete</MenuItem>
							)}
						</>
					)}
				</Menu>
			</div>
        </div>
    );
};