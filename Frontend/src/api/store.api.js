import api from "./axios";

export const getNearbyStores = ({lat, lng}) => {
    return api.get("/stores/nearby", {
        params: {lat, lng}
    });
};