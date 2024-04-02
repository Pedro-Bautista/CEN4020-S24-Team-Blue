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
	Typography,
	TextField,
	Button,
	Dialog,
	DialogTitle,
	DialogContent,
	DialogContentText,
	DialogActions
} from '@mui/material'
import MoreVertIcon from '@mui/icons-material/MoreVert';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export const Jobs = () => {
	const { user } = AuthData();
	const [appliedJobs, setAppliedJobs] = useState([]);
	const [savedJobs, setSavedJobs] = useState([]);
	const [activeTab, setActiveTab] = useState('all'); // 'all', 'my', or 'saved', 'applied', 'not applied'
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

	const [openApplyDialog, setOpenApplyDialog] = useState(false);
	const [applicationData, setApplicationData] = useState({
		job_id: '',
		graduation_date: '',
		start_working_date: '',
		application_paragraph: ''
	});

	// State variable to hold the count of applied jobs
	const [appliedJobsCount, setAppliedJobsCount] = useState(0);

	const handleOpenApplyDialog = (jobId) => {
		setApplicationData(prevData => ({ ...prevData, job_id: jobId }));
		setOpenApplyDialog(true);
	};

	const handleApply = async (e) => {
		e.preventDefault();
		try {
			await api.applyToJob(applicationData);
			setOpenApplyDialog(false);
			setApplicationData({ job_id: '', graduation_date: '', start_working_date: '', application_paragraph: '' });
			// No need to update applied jobs count here
		} catch (error) {
			console.error('Error applying to job:', error);
			setMessage('Failed to apply to job. Please try again.');
		}
	};

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

		const fetchAppliedJobs = async () => {
			try {
				const fetchedAppliedJobs = await api.fetchAppliedJobs();
				setAppliedJobs(fetchedAppliedJobs);
				// Update the count of applied jobs
				setAppliedJobsCount(fetchedAppliedJobs.length);
				// Show alert to the user
				alert(`You have applied for ${fetchedAppliedJobs.length} job(s).`);
			} catch (error) {
				console.error('Error fetching applied jobs:', error);
			}
		};

		fetchAppliedJobs();
		fetchJobs();
		fetchSavedJobs();
	}, []);

	// Rest of the component code...
};
