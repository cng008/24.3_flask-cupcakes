const BASE_URL = 'http://127.0.0.1:5000/api';
// http://localhost:5000/api

// GENERATE CUPCAKE HTML
function generateCupcakeHTML(cupcake) {
  return `
    <div class="col-3">
      <div class="card bg-light my-4" data-cupcake-id=${cupcake.id}>
          <img class="card-img-top" src="${cupcake.image}" alt="(no image provided)" style="width:10fr;height:200px;object-fit:cover;">
        <div class="card-body">
            <p class="card-text">
                Flavor: ${cupcake.flavor} <br> Size: ${cupcake.size} <br> Rating: ${cupcake.rating} <br>
                <button class="delete-btn btn btn-warning btn-sm text-light mt-2">Remove</button>
            </p>
        </div>
      </div>
    </div>
    `;
}

// PUT INITIAL CUPCAKES ON PAGE
async function fetchAllCupcakes() {
  const res = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of res.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $('#list').append(newCupcake);
  }
}

// HANDLE FORM FOR ADDING NEW CUPCAKES
$('#new-cupcake-form').on('submit', addCupcake);

async function addCupcake(e) {
  e.preventDefault();
  let flavor = $('#cupcakeFlavor').val();
  let size = $('#cupcakeSize').val();
  let rating = $('#cupcakeRating').val();
  let image = $('#cupcakeImage').val();

  const res = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  let newCupcake = $(generateCupcakeHTML(res.data.cupcake));
  $('#list').append(newCupcake);
  $('#new-cupcake-form').trigger('reset');
}

// HANDLE DELETE CUPCAKES
$('#list').on('click', '.delete-btn', deleteCupcake);

async function deleteCupcake(e) {
  e.preventDefault();
  let $cupcake = $(e.target).parent().parent().parent();
  let cupcakeId = $cupcake.attr('data-cupcake-id');

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
}

$(fetchAllCupcakes);
