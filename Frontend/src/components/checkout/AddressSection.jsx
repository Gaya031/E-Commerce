import React from 'react'

const ADDRESSES = [
  {
    id: 1,
    label: "Home",
    name: "Rahul Sahu",
    address: "123 Green St, Block B, Springfield Gardens",
    city: "Bangalore, KA 560001",
    phone: "+91 98765 43210",
    default: true,
  },
  {
    id: 2,
    label: "Office",
    name: "Rahul Sahu",
    address: "45 Tech Park, Outer Ring Road",
    city: "Bangalore, KA 560103",
    phone: "+91 98765 43210",
    default: false,
  },
];


const AddressSection = () => {
  const [selected, setSelected] = useState(1);

  return (
    <div className="bg-white p-6 rounded-xl">
      <div className="flex justify-between mb-4">
        <h2 className="font-semibold">1. Shipping Address</h2>
        <button className="text-green-600 text-sm">Add New Address</button>
      </div>

      <div className="space-y-4">
        {ADDRESSES.map(addr => (
          <div
            key={addr.id}
            onClick={() => setSelected(addr.id)}
            className={`border rounded-xl p-4 cursor-pointer ${
              selected === addr.id
                ? "border-green-500 bg-green-50"
                : "border-gray-200"
            }`}
          >
            <div className="flex justify-between">
              <p className="font-medium">{addr.label}</p>
              {addr.default && (
                <span className="text-xs bg-green-500 text-white px-2 py-1 rounded">
                  Default
                </span>
              )}
            </div>
              <p className="text-sm mt-1">{addr.name}</p>
            <p className="text-sm">{addr.address}</p>
            <p className="text-sm">{addr.city}</p>
            <p className="text-sm">Phone: {addr.phone}</p>
          </div>
        ))}
      </div>

      <div className="mt-4 bg-gray-200 h-32 rounded flex items-center justify-center">
        📍 Edit on Map
      </div>
    </div>
  );
}

export default AddressSection