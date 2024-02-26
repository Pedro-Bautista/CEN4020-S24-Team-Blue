import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000'

const api = axios.create({
  	baseURL: API_BASE_URL,
  	headers: {
    	'Content-Type': 'application/json',
		'token': localStorage.getItem('token')
  	},
})

const login = async (userData) => {
    try {
        const response = await api.post('/login', userData)
        return response
    } catch (error) {
		console.log(error)
        throw error
    }
}

const signup = async (userData) => {
    try {
        const response = await api.post('/signup', userData)
        return response
    } catch (error) {
		console.log(error)
        throw error
    }
}

const searchForPeople = async (searchData) => {
    try {
        const response = await api.post('/user_search', searchData);
        return response.data;
    } catch (error) {
        console.log(error);
        throw error;
    }
};

const postJob = async (jobData) => {
	try {
		const response = await api.post('/job_post', jobData);
		return response.data;
	} catch (error) {
		console.log(error);
		throw error;
	}
};

const updatePref = async (prefData) => {
    
	try {
		const response = await api.post('/update_preferences', prefData);
		return response.data;
	} catch (error) {
		console.log(error);
		throw error;
	}
};

const requestConnection = async (requestData) => {

	try {
		const response = await api.post('/send_request', requestData);
		return response.data
	} catch (error) {
		console.log(error);
		throw error;
	}
};

// potentially need data parameter here 
const getRequests = async () => {

	try {
		const response = await api.post('/get_requests_list');
		return response.data
	} catch (error) {
		console.log(error);
		throw error;
	}
};


export default {
	login,
	signup,
	searchForPeople,
	postJob,
    updatePref,
	requestConnection,
	getRequests,
}