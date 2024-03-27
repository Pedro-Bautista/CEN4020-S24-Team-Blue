import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';
import { useParams } from 'react-router-dom';
import api from '../api/api';

const ChatWindow = ({ chatId, userId }) => {
	const [messages, setMessages] = useState([]);
	const [newMessage, setNewMessage] = useState('');
	const endOfMessagesRef = useRef(null);

	useEffect(() => {
		const fetchMessages = async () => {
			const data = await api.fetchMessages(chatId);
			setMessages(data);
			scrollToBottom();
		};

		fetchMessages();
	}, [chatId]);

	const scrollToBottom = () => {
		endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
	};

	const handleSend = async () => {
		if (!newMessage.trim()) return;
		await api.sendMessage({ chat_id: chatId, content: newMessage });

		setNewMessage('');

		const data = await api.fetchMessages(chatId);
		setMessages(data);
	};

	return (
		<Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', p: 2 }}>
			<Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2 }}>
				{messages.map((msg, index) => (
					<Paper
						key={index}
						elevation={1}
						sx={{
							p: 1,
							mb: 1,
							border: '1px solid rgba(0,0,0,0.12)',
							backgroundColor: msg.user_id === userId ? 'rgba(63, 81, 181, 0.05)' : '#fff',
							alignSelf: msg.user_id === userId ? 'flex-end' : 'flex-start',
							maxWidth: '75%',
							ml: msg.user_id === userId ? 'auto' : 0,
							mr: msg.user_id === userId ? 0 : 'auto',
						}}
					>
						<Typography variant="body2">{msg.content}</Typography>
					</Paper>
				))}
				<div ref={endOfMessagesRef}></div>
			</Box>
			<Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
				<TextField
					fullWidth
					variant="outlined"
					value={newMessage}
					onChange={(e) => setNewMessage(e.target.value)}
					placeholder="Type a message..."
					sx={{ mr: 1 }}
				/>
				<Button onClick={handleSend} variant="contained">Send</Button>
			</Box>
		</Box>
	);
}

export default ChatWindow;