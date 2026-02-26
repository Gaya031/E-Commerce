import api from "./axios";

export const getNotifications = (page = 1, size = 20) => {
    return api.get("/notifications", {
        params: { page, size }
    });
};

export const getUnreadCount = () => {
    return api.get("/notifications/unread-count");
};

export const markAsRead = (notificationId) => {
    return api.patch(`/notifications/${notificationId}/read`);
};

export const markAllAsRead = () => {
    return api.post("/notifications/read-all");
};

export const deleteNotification = (notificationId) => {
    return api.delete(`/notifications/${notificationId}`);
};
