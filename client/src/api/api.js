import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000'

const api = axios.create({
  	baseURL: API_BASE_URL,
  	headers: {
    	'Content-Type': 'application/json',
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

export default {
	login,
	signup,
}