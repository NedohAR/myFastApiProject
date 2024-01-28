import React, { useState, useEffect } from 'react';
import api from './api';
import './App.css';

const App = () => {
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });

  const { name, email, password } = formData;

  const fetchUsers = async () => {
    try {
      const response = await api.get('/get_users');
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error fetching users:', error.message);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const createUser = async () => {
    try {
      await api.post('/create_user', formData);
      setFormData({
        name: '',
        email: '',
        password: '',
      });
      fetchUsers();
    } catch (error) {
      console.error('Error creating user:', error.message);
    }
  };

  // const updateUser = async (userName) => {
  //   try {
  //     await api.put(`/update_user/${userName}`, formData);
  //     fetchUsers();
  //   } catch (error) {
  //     console.error('Error updating user:', error.message);
  //   }
  // };

  const deleteUser = async (userName) => {
    try {
      await api.delete(`/delete_user/${userName}`);
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error.message);
    }
  };

  return (
    <div className="App">
      <h1>User Management App</h1>
      <form>
        <label>Name:</label>
        <input type="text" value={name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />

        <label>Email:</label>
        <input type="email" value={email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} required />

        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} required />

        <button type="button" onClick={createUser}>
          Create User
        </button>
      </form>

      <div>
        <h2>Users List</h2>
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              {`${user.name} - ${user.email}`}
              <button type="button" onClick={() => deleteUser(user.name)}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
