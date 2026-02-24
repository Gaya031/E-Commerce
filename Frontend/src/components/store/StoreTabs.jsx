import React from 'react'
import { NavLink, useParams } from 'react-router-dom';


const tabs = [
  {label: "Products", path:""},
  {label: "Reviews", path: "reviews"},
  {label: "Promotions", path: "promotions"},
  {label: "About", path: "about"},
];

const StoreTabs = () => {
  const {storeId } = useParams();
  return (
    <div className="bg-white border-b">
      <div className="max-w-7xl mx-auto px-4 flex gap-6">
        {tabs.map(tab => (
          <NavLink
            key={tab.label}
            to={`/store/${storeId}/${tab.path}`}
            end={tab.path === ""}
            className={({ isActive }) =>
              `py-4 text-sm font-medium ${
                isActive
                  ? "border-b-2 border-blue-600 text-blue-600"
                  : "text-gray-500"
              }`
            }
          >
            {tab.label}
          </NavLink>
        ))}
      </div>
    </div>
  )
}

export default StoreTabs