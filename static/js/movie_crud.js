import { EntityCRUD } from './entity_crud.js';

class MovieCRUD extends EntityCRUD {
  constructor() {
    super('movies', 'movie-form', 'movie-list', 'prev-movie-page', 'next-movie-page');
  }

  display(movies) {
    this.list.innerHTML = movies.map((movie) => `
        <tr>
          <td>${movie.title}</td>
          <td>${movie.release_date}</td>
          <td>
            <button onclick="movieCRUD.update(${movie.id}, /* updatedData */)">Update</button>
            <button onclick="movieCRUD.delete(${movie.id})">Delete</button>
          </td>
        </tr>
      `).join('');
  }

  getFormData() {
    return {
      title: document.getElementById('movie-title').value,
      release_date: document.getElementById('movie-release-date').value
    };
  }
}

export { MovieCRUD };
