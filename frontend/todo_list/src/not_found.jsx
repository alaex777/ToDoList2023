import { Container, Typography } from '@mui/material'
import React from 'react'
import MyHeader from './header'

const NotFound = () => {
    return <div style={{padding:'5px'}}>
        <MyHeader/>
        <Container sx={{padding: '10px'}}>
            <Typography component='h1'>The page you are trying to found doesn't exist :(</Typography>
        </Container>
    </div>
}

export default NotFound