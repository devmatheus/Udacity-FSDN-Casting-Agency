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
            <button class="btn btn-sm btn-danger delete-button" onclick="crudInstance.delete(${movie.id})">Delete</button>
          </td>
        </tr>
      `).join('');
  }

  populateForm(item) {
    super.populateForm(item);

    if (this.form) {
        const actorsSelect = document.getElementById('actors');
        if (actorsSelect) {
            const movieActorIds = item.actors.map((actor) => actor.id);
            for (const option of actorsSelect.options) {
                option.selected = movieActorIds.includes(parseInt(option.value));
            }

            $(actorsSelect).select2().trigger('change');
        }
    }
}

  getFormData() {
    return {
      title: document.getElementById('title').value,
      release_date: document.getElementById('release_date').value,
      actors: Array.from(document.getElementById('actors').selectedOptions).map(option => option.value)
    };
  }
}

export { MovieCRUD };
