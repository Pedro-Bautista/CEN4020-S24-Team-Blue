import React, { useState, useEffect } from 'react'
import { AuthData } from '../auth/AuthWrapper'
import ChatList from './ChatList'
import ChatWindow from './ChatWindow'
import api from '../api/api'
import {
	Grid,
	Divider
} from '@mui/material'

export const Chats = () => {
	const [chats, setChats] = useState([]);
	const [currentChat, setCurrentChat] = useState(null);
	const { user } = AuthData();

	useEffect(() => {
		const fetchChats = async () => {
			const data = await api.getChatList();
			setChats(data);
		};

		fetchChats();
	}, []);

	return (
		<Grid container spacing={1} sx={{ height: '70vh', width: '100%' }}>
			<Grid item xs={4} sx={{ overflowY: 'auto', borderRight: '1px solid rgba(0, 0, 0, 0.12)', pr: 2}}>
				<ChatList chats={chats} setChats={setChats} setCurrentChat={setCurrentChat} />
			</Grid>
			<Grid item xs={8} sx={{ overflowY: 'auto' }}>
				{currentChat && <ChatWindow chatId={currentChat} userId={user.id} />}
			</Grid>
		</Grid>
	);
}