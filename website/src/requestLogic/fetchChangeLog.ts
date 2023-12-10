import { ChangelogData } from "@/types/Change";
import api from '@/services/AxiosInterceptor';

export default async function fetchChangeLogData(page: number, pageSize: number, search?: string, searchColumn?: string): Promise<ChangelogData>{

    let searchQuery = search !== undefined ? `/edit/history?limit=${pageSize}&page=${page}&search=${search}` : `/edit/history?limit=${pageSize}&page=${page}`

    if(search !== undefined && searchColumn !== undefined){
        searchQuery += `&search_column=${searchColumn}`
    }
    const changeLogData = await api.get<ChangelogData>(
        searchQuery
    );

    return changeLogData.data;

}