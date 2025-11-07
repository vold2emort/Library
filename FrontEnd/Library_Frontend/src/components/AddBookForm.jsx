import React, { useState } from "react";

function AddBookForm() {
  const [book, setBook] = useState({
    title: "",
    author: "",
    published_date: "",
    available: true,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setBook({ ...book, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("http://127.0.0.1:8000/api/books/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(book),
    })
      .then((res) => res.json())
      .then(() => alert("Book added successfully!"))
      .catch((err) => console.error(err));
  };

  return (
    <div className="card p-4 shadow-sm">
      <h3 className="mb-3">Add New Book</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Title</label>
          <input name="title" className="form-control" onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Author</label>
          <input name="author" className="form-control" onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Published Date</label>
          <input type="date" name="published_date" className="form-control" onChange={handleChange} required />
        </div>
        <div className="form-check mb-3">
          <input
            className="form-check-input"
            type="checkbox"
            name="available"
            checked={book.available}
            onChange={handleChange}
          />
          <label className="form-check-label">Available</label>
        </div>
        <button type="submit" className="btn btn-primary">Add Book</button>
      </form>
    </div>
  );
}

export default AddBookForm;
