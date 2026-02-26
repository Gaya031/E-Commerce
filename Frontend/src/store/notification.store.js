import { create } from 'zustand';
import { getNotifications, getUnreadCount, markAsRead, markAllAsRead, deleteNotification } from '../api/notification.api';

export const useNotificationStore = create((set, get) => ({
    notifications: [],
    unreadCount: 0,
    isLoading: false,
    error: null,
    
    fetchNotifications: async (page = 1, size = 20) => {
        set({ isLoading: true, error: null });
        try {
            const response = await getNotifications(page, size);
            set({ notifications: response.data, isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },
    
    fetchUnreadCount: async () => {
        try {
            const response = await getUnreadCount();
            set({ unreadCount: response.data.unread_count });
        } catch (error) {
            console.error('Failed to fetch unread count:', error);
        }
    },
    
    markNotificationAsRead: async (notificationId) => {
        try {
            await markAsRead(notificationId);
            const { notifications, unreadCount } = get();
            set({
                notifications: notifications.map(n => 
                    n.id === notificationId ? { ...n, is_read: true } : n
                ),
                unreadCount: Math.max(0, unreadCount - 1)
            });
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
        }
    },
    
    markAllNotificationsAsRead: async () => {
        try {
            await markAllAsRead();
            const { notifications } = get();
            set({
                notifications: notifications.map(n => ({ ...n, is_read: true })),
                unreadCount: 0
            });
        } catch (error) {
            console.error('Failed to mark all notifications as read:', error);
        }
    },
    
    removeNotification: async (notificationId) => {
        try {
            await deleteNotification(notificationId);
            const { notifications, unreadCount } = get();
            const notification = notifications.find(n => n.id === notificationId);
            set({
                notifications: notifications.filter(n => n.id !== notificationId),
                unreadCount: notification && !notification.is_read ? Math.max(0, unreadCount - 1) : unreadCount
            });
        } catch (error) {
            console.error('Failed to delete notification:', error);
        }
    }
}));
