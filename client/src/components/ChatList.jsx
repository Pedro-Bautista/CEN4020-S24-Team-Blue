import React, { useState, useEffect } from 'react';
import api from '../api/api';
import {
	List,
	ListItemButton,
	ListItem,
	ListItemText,
	Button,
	Accordion,
	AccordionSummary,
	AccordionDetails,
	Typography,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const ChatList = ({ chats, setChats, setCurrentChat }) => {
	const [people, setPeople] = useState([]);

	useEffect(() => {
		const fetchPeople = async () => {
			const data = await api.getAcceptedProfiles({});
			setPeople(data);
		};

		const fetchChats = async () => {
			const data = await api.getChatList();
			setChats(chats);
		}

		fetchPeople();
		fetchChats();
	}, []);

	const handleCreateChat = async (user2_id) => {
		// check if chat already exists
		for (let chat of chats) {
			console.log(chat);
			if (chat.user2 == user2_id || chat.user1 == user2_id) {
				setCurrentChat(chat.chat_id);
				return;
			}
		}
		
		await api.createChat(user2_id);
		const data = await api.getChatList();
		setChats(data);
	};

	return (
		<div>
			<Accordion>
				<AccordionSummary
					expandIcon={<ExpandMoreIcon />}
					aria-controls="panel1a-content"
					id="panel1a-header"
				>
					<Typography>Connections</Typography>
				</AccordionSummary>
				<AccordionDetails>
					<List>
						{people.map((person) => (
							<ListItem key={person.user_id} secondaryAction={
								<Button variant="contained" onClick={() => handleCreateChat(person.user_id)}>Chat</Button>
							}>
								<ListItemText primary={person.first_name + " " + person.last_name} />
							</ListItem>
						))}
					</List>
				</AccordionDetails>
			</Accordion>
			<List>
				{chats.map((chat) => (
					<ListItemButton key={chat.chat_id} onClick={() => setCurrentChat(chat.chat_id)}>
						<ListItemText primary={chat.user2} />
					</ListItemButton>
				))}
			</List>
		</div>
	);
};

export default ChatList;