import { ChangelogData } from "@/types/Change";
import api from '@/services/AxiosInterceptor';

export default async function fetchChangeLogData(page: number, pageSize: number): Promise<ChangelogData>{

    const changeLogData = await api.get<ChangelogData>(
        `/edit/history?limit=${pageSize}&page=${page}`
    );

    return changeLogData.data;

}