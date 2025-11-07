import React, { useEffect, useState } from "react";

function Books() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/")
      .then((res) => res.json())
      .then((data) => setBooks(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2 className="mb-4">📖 Book List</h2>
      <table className="table table-striped table-hover">
        <thead className="table-primary">
          <tr>
            <th>Title</th><th>Author</th><th>Published</th><th>Status</th>
          </tr>
        </thead>
        <tbody>
          {books.map((b) => (
            <tr key={b.id}>
              <td>{b.title}</td>
              <td>{b.authors}</td>
              {/* <td>{b.published_date}</td> */}
              {/* <td>
                <span className={`badge ${b.available ? "bg-success" : "bg-danger"}`}>
                  {b.available ? "Available" : "Borrowed"}
                </span>
              </td> */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Books;
