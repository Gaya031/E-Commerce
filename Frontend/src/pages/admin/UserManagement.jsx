import { useEffect, useState } from "react";
import { blockUser, getAdminUsers } from "../../api/admin.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AdminUserManagement() {
  const [users, setUsers] = useState([]);

  const load = async () => {
    const res = await getAdminUsers();
    setUsers(res.data || []);
  };

  useEffect(() => {
    let active = true;
    getAdminUsers().then((res) => {
      if (active) setUsers(res.data || []);
    });
    return () => {
      active = false;
    };
  }, []);

  const toggleBlock = async (user) => {
    await blockUser(user.id, { blocked: !user.is_blocked });
    await load();
  };

  return (
    <RoleDashboardLayout role="admin" title="User Management">
      <div className="max-w-6xl">
        <div className="bg-white rounded-xl shadow p-4 space-y-2">
          {users.map((u) => (
            <div key={u.id} className="flex justify-between border rounded p-3">
              <div>
                <p className="font-medium">{u.name} ({u.role})</p>
                <p className="text-sm text-gray-500">{u.email}</p>
              </div>
              <button onClick={() => toggleBlock(u)} className="px-3 py-1 rounded bg-gray-900 text-white">
                {u.is_blocked ? "Unblock" : "Block"}
              </button>
            </div>
          ))}
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
