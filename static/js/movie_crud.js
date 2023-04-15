import { EntityCRUD } from './entity_crud.js';

class MovieCRUD extends EntityCRUD {
  constructor() {
    super('movies', 'movie-form', 'movie-list', 'prev-movie-page', 'next-movie-page');
  }

  display(movies) {
    if (!this.list) return;

    this.list.innerHTML = movies.map((movie) => `
        <tr>
          <td>${movie.title}</td>
          <td>${movie.release_date}</td>
          <td>
            <button onclick="crudInstance.edit(${movie.id})">Edit</button>
            <button onclick="crudInstance.delete(${movie.id})">Delete</button>
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
