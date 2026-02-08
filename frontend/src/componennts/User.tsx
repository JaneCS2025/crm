import { useEffect, useState } from "react";
import { fetchUsers, createUser, updateUser, deleteUser } from "../api/api";

const emptyForm = {
  first_name: "",
  last_name: "",
  email: "",
  tel: "",
  password: "",
};

export default function User() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      const data = await fetchUsers();
      setUsers(data);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  function onChange(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  }

  function startEdit(u) {
    setEditingId(u.id);
    setForm({
      first_name: u.first_name,
      last_name: u.last_name,
      email: u.email,
      tel: u.tel || "",
      password: "", // optional on update
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function onSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      if (editingId) {
        // Send only fields; password optional
        const patch = {
          first_name: form.first_name,
          last_name: form.last_name,
          email: form.email,
          tel: form.tel,
          ...(form.password ? { password: form.password } : {}),
        };
        await updateUser(editingId, patch);
      } else {
        await createUser(form);
      }
      cancelEdit();
      await load();
    } catch (e2) {
      setError(e2.message);
    }
  }

  async function onDelete(id) {
    setError("");
    try {
      await deleteUser(id);
      await load();
    } catch (e) {
      setError(e.message);
    }
  }

  

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>User Info Details</h2>

      {error && (
        <div style={{ padding: 12, background: "#ffe5e5", marginBottom: 16 }}>
          {error}
        </div>
      )}

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 8, marginBottom: 24 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
          <input name="first_name" placeholder="First name" value={form.first_name} onChange={onChange} required />
          <input name="last_name" placeholder="Last name" value={form.last_name} onChange={onChange} required />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
          <input name="email" placeholder="Email" value={form.email} onChange={onChange} required />
          <input name="tel" placeholder="Tel" value={form.tel} onChange={onChange} />
        </div>

        <input
          name="password"
          type="password"
          placeholder={editingId ? "New password (optional)" : "Password"}
          value={form.password}
          onChange={onChange}
          required={!editingId}
        />

        <div style={{ display: "flex", gap: 8 }}>
          <button type="submit">{editingId ? "Update User" : "Add User"}</button>
          {editingId && <button type="button" onClick={cancelEdit}>Cancel</button>}
        </div>
      </form>

      <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Tel</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id} style={{ borderBottom: "1px solid #f0f0f0" }}>
              <td>{u.id}</td>
              <td>{u.first_name} {u.last_name}</td>
              <td>{u.email}</td>
              <td>{u.tel || ""}</td>
              <td style={{ display: "flex", gap: 8 }}>
                <button onClick={() => startEdit(u)}>Edit</button>
                <button onClick={() => onDelete(u.id)}>Delete</button>
              </td>
            </tr>
          ))}
          {users.length === 0 && (
            <tr><td colSpan="5" style={{ padding: 16 }}>No users yet.</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
