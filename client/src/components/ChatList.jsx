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

			const chats = await Promise.all(data.map(async (chat) => {
				const response = await api.getUserData({ user_id: chat.user2 });
				const user2 = response.user
				return {
					id: chat.chat_id,
					name: user2.first_name + " " + user2.last_name,
				};
			}));

			console.log(chats);

			setChats(chats);
		}

		fetchPeople();
		fetchChats();
	}, []);

	const handleCreateChat = async (user2_id) => {
		await api.createChat(user2_id);
		const data = await api.getChatList();
		console.log(data)
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
					<ListItemButton key={chat.chat_id} onClick={() => setCurrentChat(chat.id)}>
						<ListItemText primary={chat.name} />
					</ListItemButton>
				))}
			</List>
		</div>
	);
};

export default ChatList;