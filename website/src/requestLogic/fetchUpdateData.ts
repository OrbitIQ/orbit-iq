import { UpdateData } from "@/types/Update";
import api from '@/services/AxiosInterceptor';

export default async function fetchUpdateData(page: number, pageSize: number, search?: string, searchColumn?: string): Promise<UpdateData>{

    let searchQuery = search !== undefined ? `/proposed/changes?limit=${pageSize}&page=${page}&search=${search}` : `/proposed/changes?limit=${pageSize}&page=${page}`

    
    if(search !== undefined && searchColumn !== undefined){
        searchQuery += `&search_column=${searchColumn}`
    }

    const updateData = await api.get<UpdateData>(
        searchQuery
    );

    const rel = updateData.data;


    return {proposed_changes: rel.proposed_changes.filter(item => item.is_approved === "denied" || item.is_approved === "pending")};

}