
import Axios from 'axios';
import { ChangelogData } from "@/types/Change";
import { editHistoryURL } from "@/Constants/constants";

export default async function fetchChangeLogData(page: number, pageSize: number): Promise<ChangelogData>{

    const changeLogData = await Axios.get<ChangelogData>(
        `${editHistoryURL}?limit=${pageSize}&page=${page}`
    );

    return changeLogData.data;

}