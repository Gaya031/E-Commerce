import api from "./axios";

export const getBanners = () => api.get("/banners/");

export const getAdminBanners = () => api.get("/banners/admin");

export const createBanner = (data) => api.post("/banners/", data);

export const updateBanner = (bannerId, data) => api.put(`/banners/${bannerId}`, data);

export const deleteBanner = (bannerId) => api.delete(`/banners/${bannerId}`);

export const uploadBannerImage = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/banners/upload-image", formData);
};
