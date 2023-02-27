import React, {useEffect, useState} from 'react'

import { Button, ListItemButton, MenuItem, Select, TextField, Typography } from '@mui/material'
import { Container } from '@mui/system'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemText from '@mui/material/ListItemText'
import ListItemAvatar from '@mui/material/ListItemAvatar'
import Avatar from '@mui/material/Avatar'
import WorkIcon from '@mui/icons-material/Work'
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart'
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball'
import AttractionsIcon from '@mui/icons-material/Attractions'
import HomeIcon from '@mui/icons-material/Home'
import DeleteIcon from '@mui/icons-material/Delete'
import PersonIcon from '@mui/icons-material/Person'
import SchoolIcon from '@mui/icons-material/School'
import MyHeader from './header'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers'
import { deleteRequest, getRequest, postRequest } from './requests'


const typeIconMap = {
    'work': <WorkIcon/>,
    'shopping': <ShoppingCartIcon/>,
    'sport': <SportsBasketballIcon/>,
    'entertainment': <AttractionsIcon/>,
    'home': <HomeIcon/>,
    'myself': <PersonIcon/>,
    'education': <SchoolIcon/>
}

const MainApp = () => {
    const [task, setTask] = useState(null)
    const [date, setDate] = useState(null)
    const [type, setType] = useState(null)

    const [tasksList, setTasksList] = useState([])

    const [error, setError] = useState(null)

    useEffect(()=>{
        getRequest('http://localhost:8000/get/tasks', setTasksList, setError)
    }, [task]) 

    if (error !== null) {
        return <div style={{padding:'5px'}}>
            <MyHeader/>
            <Container sx={{padding: '10px'}}>
                <Typography component='h1'>Oops, something has gone wrong. Error: {error}</Typography>
            </Container>
        </div>
    }

    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }

    console.log('LIST: ', tasksList)

    return <div style={{padding:'5px'}}>
        <MyHeader/>
        <Container sx={{padding: '10px'}}>
            <Container>
                <Typography component='h1'>My work:</Typography>
            </Container>
            <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
                {tasksList.map((x) => {
                    return <ListItem>
                        <ListItemAvatar>
                            <Avatar>
                                {typeIconMap[x[3]]}
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary={x[1]} secondary={x[2]} />
                        <ListItemButton edge="end" aria-label="delete" onClick={() =>
                            deleteRequest('http://localhost:8000/delete/task/'+x[0], setError)
                        }>
                            <DeleteIcon />
                        </ListItemButton>
                    </ListItem>
                })}
            </List>
            <Container sx={{padding: '10px'}}>
                <TextField 
                    id="standard-basic" 
                    label="My task" 
                    variant="standard"
                    value={task}
                    onChange={(event) => {
                        setTask(event.target.value);
                    }}
                />
            </Container>
            <Container sx={{padding: '10px'}}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                        label="Due date"
                        inputFormat="MM/dd/yyyy"
                        value={date}
                        onChange={inp=>setDate(inp)}
                        renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
            </Container>
            <Container>
                <Select
                    value={type}
                    label="Type"
                    onChange={(event)=>setType(event.target.value)}
                >
                    <MenuItem value={'work'}>Work</MenuItem>
                    <MenuItem value={'education'}>Education</MenuItem>
                    <MenuItem value={'sport'}>Sport</MenuItem>
                    <MenuItem value={'shopping'}>Shopping</MenuItem>
                    <MenuItem value={'entertainment'}>Entertainment</MenuItem>
                    <MenuItem value={'home'}>Home</MenuItem>
                    <MenuItem value={'myself'}>Myself</MenuItem>
                </Select>
            </Container>
            <Container sx={{padding: '10px'}}>
                <Button variant="contained" onClick={() => {
                    if (task !== null && date !== null && type !== null) {
                        postRequest(
                            'http://localhost:8000/create/task', 
                            setTasksList, 
                            setError, 
                            {
                                "content": task, 
                                "due_date": date.toLocaleDateString("en-US", options).toString(), 
                                "type": type
                            }
                        )
                    }
                }}>
                    Add
                </Button>
            </Container>
        </Container>
    </div>
}

export default MainApp