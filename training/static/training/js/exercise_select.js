const exercisesForm = $("#exercises-form");
const exercisesAll = exercisesForm.find("li");
const submitExercisesBtn = $("#submit-exercises-btn");
const dummy = $("#dummy");

const searchInput = $("#search-input");
const filters = $("#filters");
const fieldFilters = filters.find(".field-filter");
const areaFilter = filters.find("#filter-area");
const selectedFilter = filters.find("#filter-selected");
const clearFiltersBtn = $("#clear-filters");

$(document).ready(function() {
    updateSelectedAreasOnDummy();
    applyExerciseFilters();
    searchExerciseByName();

    exercisesForm.find("input").on("change", updateSelectedAreasOnDummy);
    submitExercisesBtn.on("click", () => { exercisesForm.submit()});

    searchInput.on("keyup", () => {
        clearExerciseFilters();
        searchExerciseByName();
    });

    filters.find("input").on("change", () => {
        clearExerciseSearch();
        applyExerciseFilters();
    });
    
    dummy.find(".area").on("click", handleDummyAreaClick);

    clearFiltersBtn.on("click", () => {
        clearExerciseFilters();
        closeExerciseFilters();
    });
})

/**
 * Updates the highlight of selected exercises' areas on the dummy.
 */
function updateSelectedAreasOnDummy() {
    exercisesForm.find("input:checked").each(function() {
        const exercise = $(this).closest(".exercise-item");
        const exerciseAreas = exercise.data("area").split(", ");
        exerciseAreas.forEach(areaName => {
            dummy.find(`.${areaName}`).addClass("selected");
        });
    });
}

/**
* Updates the highlight of filtered exercises' areas on the dummy.
*/
function updateFilteredAreasOnDummy() {
    const checkedInputs = areaFilter.find("input:checked");

    dummy.find(".area").removeClass("filtered");

    checkedInputs.each(function() {
        const areaName = $(this).val();
        const dummyArea = dummy.find(`.${areaName}`);
        dummyArea.addClass("filtered");
    })
}

/**
 * Filters all exercises based on the selected filters.
 * If no filter is selected, shows all exercises.
 */
function applyExerciseFilters() {
    const checkedInputs = filters.find("input:checked");

    if (checkedInputs.length === 0) {
        clearExerciseFilters();
        return;
    }

    const filteredExercises = filterByFields(filterBySelected(exercisesAll));

    exercisesAll.hide();
    filteredExercises.show();
    updateFilteredAreasOnDummy();
    clearFiltersBtn.show();

    function filterBySelected(exercises) {
        const checkedInputs = selectedFilter.find("input:checked");
        const filterValues = checkedInputs.toArray().map(input => $(input).val());

        if (filterValues.length === 0 || filterValues.length === 2) {
            return exercises;
        }

        const filterValue = filterValues[0] === "true";

        exercises = exercises.filter(function() {
            const exerciseValue = $(this).find('input').is(":checked"); 
            return exerciseValue === filterValue;
        });

        return exercises;
    }

    function filterByFields(exercises) {
        fieldFilters.each(function() {
            const filterName = $(this).data("name");
            const checkedInputs = $(this).find("input:checked");
            const filterValues = checkedInputs.toArray().map(input => $(input).val());
            
            if (filterValues.length === 0) {
                return;
            }

            exercises = exercises.filter(function() {
                const exerciseValues = $(this).data(filterName).toString(); 
                return filterValues.some(value => exerciseValues.includes(value));
            });
        });

        return exercises;
    }
}

/**
 * Filters all exercises by name based on the search text.
 */
function searchExerciseByName() {
    const searchText = searchInput.val().toLowerCase();

    if (!searchText) {
        return;
    }

    exercisesAll.each(function() {
        const exerciseName = $(this).data("name");
        if (!exerciseName.includes(searchText)) {
            $(this).hide();
        }}
    );
}

/**
 * Handles the click event for the dummy area: 
 * toggles the highlight on the area and activates the filter. 
 */
function handleDummyAreaClick() {
    const areaName = $(this).data("area");
    const filterInput = areaFilter.find(`input[value=${areaName}]`);

    filterInput.trigger("click");
}

function clearExerciseSearch() {
    searchInput.val("");
    exercisesAll.show();
}

/**
 * Clears all filters and shows all exercises.
 */
function clearExerciseFilters() {
    filters.find("input").prop("checked", false);
    exercisesAll.show();
    dummy.find(".area").removeClass("filtered");
    clearFiltersBtn.hide();
}

/**
 * Closes the exercise filters details elements.
 */
function closeExerciseFilters() {
    filters.find("details").prop("open", false);
}
