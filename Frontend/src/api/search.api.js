import api from "./axios";

export const searchAll = query => {
    return apo.get("/search", {
        params: {q: query}
    });
};