export const getRoleHomePath = (role) => {
  switch (role) {
    case "seller":
      return "/seller";
    case "admin":
      return "/admin";
    case "delivery":
      return "/delivery";
    default:
      return "/";
  }
};
