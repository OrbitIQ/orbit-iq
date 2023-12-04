import Axios from 'axios';
import { proposedChangeURL } from "@/Constants/constants";
import { UpdateData } from "@/types/Update";

export default async function fetchUpdateData(page: number, pageSize: number): Promise<UpdateData>{

    const updateData = await Axios.get<UpdateData>(
        `${proposedChangeURL}?limit=${pageSize}&page=${page}`
    );

    const rel = updateData.data;

    return rel;

}