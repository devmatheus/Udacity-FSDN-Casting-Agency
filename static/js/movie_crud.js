import { EntityCRUD } from './entity_crud.js';

class MovieCRUD extends EntityCRUD {
  constructor() {
    super('movies', 'movie-form', 'movie-list', 'prev-movie-page', 'next-movie-page');
  }

  display(movies) {
    if (!this.list) return;

    this.list.innerHTML = '<tr></tr><th>Title</th><th>Release Date</th><th>Actions</th></tr>';
    this.list.innerHTML += movies.map((movie) => `
        <tr>
          <td>${movie.title}</td>
          <td>${movie.release_date_formatted}</td>
          <td>
            <button class="btn btn-sm btn-warning" onclick="crudInstance.edit(${movie.id})">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="crudInstance.delete(${movie.id})">Delete</button>
          </td>
        </tr>
      `).join('');
  }

  getFormData() {
    return {
      title: document.getElementById('title').value,
      release_date: document.getElementById('release_date').value
    };
  }
}

export { MovieCRUD };
