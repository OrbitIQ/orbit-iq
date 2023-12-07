import { UpdateData } from "@/types/Update";
import api from '@/services/AxiosInterceptor';

export default async function fetchUpdateData(page: number, pageSize: number): Promise<UpdateData>{

    const updateData = await api.get<UpdateData>(
        `/proposed/changes?limit=${pageSize}&page=${page}`
    );

    const rel = updateData.data;


    return {proposed_changes: rel.proposed_changes.filter(item => item.is_approved === "denied" || item.is_approved === "pending")};

}