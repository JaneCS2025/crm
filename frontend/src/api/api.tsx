const BASE_URL = "http://127.0.0.1:5000";

export async function fetchUsers() {
  const res = await fetch(`${BASE_URL}/api/users`);
  if (!res.ok) throw new Error("Failed to load users");
  return res.json();
}

export async function createUser(user) {
  const res = await fetch(`${BASE_URL}/api/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to create user");
  }
  return res.json();
}

export async function updateUser(id, patch) {
  const res = await fetch(`${BASE_URL}/api/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(patch),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to update user");
  }
  return res.json();
}

export async function deleteUser(id) {
  const res = await fetch(`${BASE_URL}/api/users/${id}`, { method: "DELETE" });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to delete user");
  }
  return res.json();
}
