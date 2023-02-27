import './App.css';

import React from 'react'
import {Route, BrowserRouter as Router, Routes} from 'react-router-dom';
import MainApp from './main';
import NotFound from './not_found';

import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const App = () => {
    return <ThemeProvider theme={darkTheme}>
        <CssBaseline/>
        <Router>
          <Routes>
            <Route path='/' element={<MainApp/>} />
            <Route path='*' element={<NotFound/>} />
          </Routes>
        </Router>
      </ThemeProvider>
  }

export default App;
