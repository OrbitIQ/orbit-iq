import SearchIcon from '@mui/icons-material/Search';
import ProgressButton from './ProgressButton';

export default function SearchButton({searchActive, handleClick}: {searchActive: Boolean, handleClick: any}){
    if(!searchActive){
        return(<SearchIcon className="ml-2" fontSize='large' onClick={handleClick}/>);
    }
    return (
        <ProgressButton/>
    );
}
