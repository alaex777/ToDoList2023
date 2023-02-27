import React from 'react'

import { AppBar, Toolbar, Typography } from '@mui/material'
import { Container } from '@mui/system';
import ListAltIcon from '@mui/icons-material/ListAlt'

const MyHeader = () => {
    return <AppBar position='static'>
        <Container>
            <Toolbar>
                <ListAltIcon/>
                <Typography component='h2'>ToDo List</Typography>
            </Toolbar>
        </Container>
    </AppBar>
}

export default MyHeader
