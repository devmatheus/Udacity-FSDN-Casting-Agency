import { EntityCRUD } from './entity_crud.js';

class ActorCRUD extends EntityCRUD {
  constructor() {
    super('actors', 'actor-form', 'actor-list', 'prev-actor-page', 'next-actor-page');
  }

  display(actors) {
    if (!this.list) return;

    // Clear the existing content
    this.list.innerHTML = '';

    // Create the table header
    const thead = `
      <thead>
        <tr>
          <th>Name</th>
          <th>Bio</th>
          <th>Actions</th>
        </tr>
      </thead>
    `;
    this.list.insertAdjacentHTML('beforeend', thead);

    // Create table body
    const tbody = document.createElement('tbody');
    actors.forEach((actor) => {
      const tr = document.createElement('tr');

      tr.innerHTML = `
          <td>${actor.name}</td>
          <td>${actor.bio}</td>
          <td>
            <button class="btn btn-sm btn-warning" onclick="crudInstance.edit(${actor.id})">Edit</button>
            <button class="btn btn-sm btn-danger delete-button" onclick="crudInstance.delete(${actor.id})">Delete</button>
          </td>
        `;
      tbody.appendChild(tr);
    });

    this.list.appendChild(tbody);
  }

  getFormData() {
    return {
      name: document.getElementById('name').value,
      bio: document.getElementById('bio').value
    };
  }
}

export { ActorCRUD };
