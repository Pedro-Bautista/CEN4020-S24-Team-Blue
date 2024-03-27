import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';
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
		<Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
			<Box sx={{ flexGrow: 1, overflowY: 'auto' }}>
				{messages.map((msg, index) => (
					<Box key={index} sx={{ textAlign: msg.user_id === userId ? 'right' : 'left' }}>
						<Typography>{msg.text}</Typography>
					</Box>
				))}
				<div ref={endOfMessagesRef}></div>
			</Box>
			<Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', padding: 1 }}>
				<TextField
					fullWidth
					variant="outlined"
					value={newMessage}
					onChange={(e) => setNewMessage(e.target.value)}
					placeholder="Type a message..."
				/>
				<Button onClick={handleSend}>Send</Button>
			</Box>
		</Box>
	);
}

export default ChatWindow;