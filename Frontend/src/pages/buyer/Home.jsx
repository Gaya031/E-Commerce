

import React from 'react'
import { useAuthStore } from '../../store/auth.store'

const Home = () => {
    const user = useAuthStore(s => s.user);
    if(!user){
        return <h2>Loading user data...</h2>;
    }
    console.log("User in Home: ", user);

  return (
    <div className='p-20'>
        <h1>Welcome</h1>
        <h2>Logged in user details</h2>
        <p>
            <strong>Name: </strong>{user.name}
        </p>
        <p>
            <strong>Email: </strong>{user.email}
        </p>
        <p>
        <strong>Role:</strong> {user.role}
      </p>

      <p>
        <strong>Wallet Balance:</strong> ₹{user.wallet_balance}
      </p>

      <p>
        <strong>Status:</strong>{" "}
        {user.is_blocked ? "Blocked ❌" : "Active ✅"}
      </p>
    </div>
  )
}

export default Home