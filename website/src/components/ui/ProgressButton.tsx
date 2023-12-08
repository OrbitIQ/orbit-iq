import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

export default function ProgressButton(){
    return (
         <Box className="ml-2" sx={{ display: 'flex' }}>
            <CircularProgress />
        </Box>
    )
}