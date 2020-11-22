$(function () {
	const cardInfos = $(".small-box")
	const cardCategories = $("#card-categories");
	const templateHtmlCardCategory = (category, htmlExpenses) => `
          <div class="col-xl-6">
              <div class="card">
                  <div class="card-header">
                      <h3 contenteditable class="category card-title">${category.name}</h3>
                      <div class="card-tools">
                          <button type="button" class="btn btn-tool delete-category" data-toggle="modal" data-target="#modal-delete-category" data-category-id="${category.id}">
                              <i class="fas fa-times" style="color: #adb5bd"></i>
                          </button>
                      </div>
                  </div>
                  <!-- /.card-header -->
                  <div class="card-body p-0">
                      <table class="table table-striped text-center">
                          <thead>
                              <tr>
                                  <th style="width: 5%">#</th>
                                  <th style="width: 45%">Name</th>
                                  <th style="width: 20%">Cost</th>
                                  <th style="width: 25%">Expected Cost</th>
                                  <th></th>
                              </tr>
                          </thead>
                          <tbody class="category-tbody">
                          	${htmlExpenses}
							${htmlAddExpense}
                          </tbody>
                      </table>
                  </div>
                  <!-- /.card-body -->
              </div>
              <!-- /.card -->
          </div>
      `;
	const templateHtmlTrExpense = (expense, number) => `
      <tr>
        <td>${number}.</td>
        <td class="expense"><span contenteditable class="name">${expense.name}</span></td>
        <td class="expense"><span contenteditable class="cost">${expense.cost}</span>$</td>
        <td class="expense"><span contenteditable class="expected-cost">${expense.expected_cost}</td>
        <td class="td-delete">
          <button type="button" class="btn bg-danger btn-sm btn-delete-expense"  data-expense-id="${expense.id}">
            <i class="fas fa-times"></i>
          </button>
        </td>
      </tr>
      `;
	const htmlTrAddExpense = `
	<tr>
		<td></td>
		<td><input class="form-control text-center new-expense-name" type="text"></td>
		<td><input class="form-control text-center new-expense-cost" type="number" step="0.01"></td>
		<td><input class="form-control text-center new-expense-expected-cost" type="number" step="0.01"></td>
		<td>
		<button type="button" class="btn bg-info btn-sm btn-add-expense">
			<i class="fas fa-plus"></i>
		</button>
		</td>
	</tr>
	`
	const htmlTableAddCategory = `
      <div class="col-xl-6">
          <div class="card">
              <div class="card-header">
                  <h3 class="card-title">&#8203;</h3>
              </div>
              <!-- /.card-header -->
              <div class="card-body p-0">
                  <table class="table table-striped text-center">
                      <thead>
                          <tr>
                              <th style="width: 5%">#</th>
                              <th style="width: 45%">Title</th>
                              <th style="width: 20%">Cost</th>
                              <th style="width: 25%">Day due</th>
                              <th></th>
                          </tr>
                      </thead>
                      <tbody class="new-category-tbody">
                          <tr>
                              <td></td>
                              <td></td>
                              <td></td>
                              <td></td>
                              <td></td>
                          </tr>
                      </tbody>
                  </table>
              </div>
              <!-- /.card-body -->
              <div class="overlay">
                  <button type="button" class="btn" data-toggle="modal" data-target="#modal-new-category">
                      <i class="fa fa-2x fa-plus" aria-hidden="true"></i>
                  </button>
              </div>
          </div>
          <!-- /.card -->
      </div>
  `;
	const Toast = Swal.mixin({
		toast: true,
		position: "top-end",
		showConfirmButton: false,
		timer: 3500,
	});


	// GET budget-info
	function userBudgetInfo() {
		var jqXHR = $.ajax({
			url: "http://127.0.0.1:8000/api/budget-info/",
			type: "GET",
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			error: function (jqXHR, textStatus, errorThrown) {
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			},
			async: false,
		});
		return jqXHR.responseJSON;
	}

	function updateUserInfoCards() {
		let budgetInfo = userBudgetInfo()
		console.log(budgetInfo)
		cardInfos.find("#daily-spendable").html(budgetInfo["daily_spendable"])
		cardInfos.find("#monthly-spendable").html(budgetInfo["monthly_spendable"])
		cardInfos.find("#month-money-left").html(budgetInfo["month_money_left"])
		cardInfos.find("#month-expenses").html(budgetInfo["month_expenses"])
	}

	// GET user-categories
	function userCategoriesList() {
		var jqXHR = $.ajax({
			url: "http://127.0.0.1:8000/api/user-monthly-categories/",
			type: "GET",
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			error: function (jqXHR, textStatus, errorThrown) {
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			},
			async: false,
		});
		return jqXHR.responseJSON;
	}

	// Update category tables
	function userCategoryTables() {
		let categories = userCategoriesList(),
			htmlTableCategories = '<div class="row">';

		cardCategories.empty();
		for (let i = 0; i < categories.length; i++) {
			let category = categories[i],
				htmlExpenses = "";
			for (let j = 0; j < category.expenses.length; j++) {
				let expense = category.expenses[j];
				if (expense.expected_cost == null) {
					expense.expected_cost = "</span>";
				} else {
					expense.expected_cost = `${expense.expected_cost}</span>$`;
				}
				htmlExpenses += templateHtmlTrExpense(expense, j + 1);
			}
			if (category.expenses.length < 20) {
				htmlAddExpense = htmlTrAddExpense
			} else {
				htmlAddExpense = ''
			}
			htmlTableCategories += templateHtmlCardCategory(category, htmlExpenses, htmlAddExpense);
		}
		if (categories.length < 16) {
			cardCategories.append(
				htmlTableCategories + htmlTableAddCategory + "</div>"
			);
		} else {
			cardCategories.append(htmlTableCategories + "</div>");
		}
		updateUserInfoCards()
	}

	// POST categories
	$(document).on("click", "#btn-sumbit-category", function (e) {
		$.ajax({
			url: "http://127.0.0.1:8000/api/categories/",
			type: "POST",
			data: JSON.stringify({
				user: $("#id-user").val(),
				name: $("#new-name-category").val(),
				monthly: true,
			}),
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			success: function () {
				userCategoryTables();
				Toast.fire({
					icon: "success",
					title: `Successfully created category ${$(
						"#new-name-category"
					).val()}!`,
				});
				$("#new-name-category").val("");
			},
			error: function (jqXHR, textStatus, errorThrown) {
				if (jqXHR.responseJSON) {
					let errorResponse = "";
					for (let [key, item] of Object.entries(jqXHR.responseJSON)) {
						if (Array.isArray(item)) {
							for (const error of item) {
								errorResponse += `${key}: ${error}<br>`;
							}
						} else {
							errorResponse += `${item}<br>`;
						}
					}
					Toast.fire({
						icon: "error",
						title: errorResponse,
					});
				} else {
					Toast.fire({
						icon: "error",
						title: "Error",
					});
				}
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			},
		});
	});

	$(document).on("click", ".btn.btn-tool.delete-category", function (e) {
		let categoryId = $(e.currentTarget).data("category-id");
		$("#btn-delete-category").data("category-id", categoryId);
	});

	// DELETE categories
	$(document).on("click", "#btn-delete-category", function (e) {
		$.ajax({
			url: `http://127.0.0.1:8000/api/categories/${$(e.currentTarget).data(
				"category-id"
			)}`,
			type: "DELETE",
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			success: function () {
				userCategoryTables();
				Toast.fire({
					icon: "success",
					title: `Successfully deleted!`,
				});
				$("#new-name-category").val("");
			},
			error: function (jqXHR, textStatus, errorThrown) {
				if (jqXHR.responseJSON) {
					let errorResponse = "";
					for (let [key, item] of Object.entries(jqXHR.responseJSON)) {
						if (Array.isArray(item)) {
							for (const error of item) {
								errorResponse += `${key}: ${error}<br>`;
							}
						} else {
							errorResponse += `${item}<br>`;
						}
					}
					Toast.fire({
						icon: "error",
						title: errorResponse,
					});
				} else {
					Toast.fire({
						icon: "error",
						title: "Error",
					});
				}
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			},
		});
	});

	// POST expenses
	$(document).on("click", ".btn-add-expense", function (e) {
		let categoryTbody = $(e.currentTarget).closest(".category-tbody"),
			cardHeader = categoryTbody.parent().parent().prev(),
			deleteCategoryBtn = cardHeader.find(".btn.btn-tool.delete-category").first(),
			expenseName = categoryTbody.find(".new-expense-name").first().val(),
			expenseCost = categoryTbody.find(".new-expense-cost").first().val(),
			expenseExpectedCost = categoryTbody.find(".new-expense-expected-cost").first().val(),
			categoryId = $(deleteCategoryBtn).data("category-id");

		if (!expenseExpectedCost) {
			expenseExpectedCost = null
		}
		$.ajax({
			url: `http://127.0.0.1:8000/api/expenses/`,
			type: "POST",
			data: JSON.stringify({
				user: $("#id-user").val(),
				name: expenseName,
				category: categoryId,
				cost: expenseCost,
				expected_cost: expenseExpectedCost,
				day_due: "",
			}),
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			success: function (jqXHR) {
				userCategoryTables();
				Toast.fire({
					icon: "success",
					title: `Successfully created ${expenseName}!`,
				});
				userCategoryTables();
			},
			error: function (jqXHR, textStatus, errorThrown) {
				if (jqXHR.responseJSON) {
					let errorResponse = "";
					for (let [key, item] of Object.entries(jqXHR.responseJSON)) {
						if (Array.isArray(item)) {
							for (const error of item) {
								errorResponse += `${key}: ${error}<br>`;
							}
						} else {
							errorResponse += `${item}<br>`;
						}
					}
					Toast.fire({
						icon: "error",
						title: errorResponse,
					});
				} else {
					Toast.fire({
						icon: "error",
						title: "Error",
					});
				}
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			},
		});
	});

	// DELETE expenses
	$(document).on("click", ".btn-delete-expense", function (e) {
		$.ajax({
			url: `http://127.0.0.1:8000/api/expenses/${$(e.currentTarget).data(
				"expense-id"
			)}/`,
			type: "DELETE",
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			success: function () {
				userCategoryTables();
				Toast.fire({
					icon: "success",
					title: `Successfully deleted!`,
				});
				userCategoryTables();
			},
			error: function (jqXHR, textStatus, errorThrown) {
				if (jqXHR.responseJSON) {
					let errorResponse = "";
					for (let [key, item] of Object.entries(jqXHR.responseJSON)) {
						if (Array.isArray(item)) {
							for (const error of item) {
								errorResponse += `${key}: ${error}<br>`;
							}
						} else {
							errorResponse += `${item}<br>`;
						}
					}
					Toast.fire({
						icon: "error",
						title: errorResponse,
					});
				} else {
					Toast.fire({
						icon: "error",
						title: "Error",
					});
				}
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			},
		});
	});

	// PATCH categories
	$(document).on("focus", "h3.category.card-title", function () {
		let $this = $(this);
		$this.data("before", $this.html());
	}).on("blur", "h3.category.card-title", function () {
		let $this = $(this)

		if ($this.data("before") != $this.html()) {
			$this.data("before"), $this.html();
			$this.trigger("change");
		}
	}).on("change", "h3.category.card-title", function () {
		let $this = $(this),
			name = $this.html(),
			id = $this.next().find("button").data("category-id");
		name = name.split("<br>")[0]

		$.ajax({
			url: `http://127.0.0.1:8000/api/categories/${id}/`,
			type: "PATCH",
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			data: JSON.stringify({ name: name }),
			success: function () {
				userCategoryTables();
				Toast.fire({
					icon: "success",
					title: `Saved changes!`,
				});
				userCategoryTables();
			},
			error: function (jqXHR, textStatus, errorThrown) {
				$this.html($this.data("before"))
				if (jqXHR.responseJSON) {
					let errorResponse = "";
					for (let [key, item] of Object.entries(jqXHR.responseJSON)) {
						if (Array.isArray(item)) {
							for (const error of item) {
								errorResponse += `${key}: ${error}<br>`;
							}
						} else {
							errorResponse += `${item}<br>`;
						}
					}
					Toast.fire({
						icon: "error",
						title: errorResponse,
					});
				} else {
					Toast.fire({
						icon: "error",
						title: "Error",
					});
				}
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			}
		});
	});


	$(document).on("click", "td.expense", function () {
		let span = $(this).find("span");
		span.focus()
	})

	// PATCH expenses
	$(document).on("focus", "span[contenteditable]", function () {
		let $this = $(this);
		$this.data("before", $this.html());
	}).on("blur", "span[contenteditable]", function () {
		let $this = $(this)

		if ($this.data("before") != $this.html()) {
			$this.data("before"), $this.html();
			$this.trigger("change");
		}
	}).on("change", "span[contenteditable]", function () {
		let $this = $(this),
			data = $this.html(),
			spanClass = $this.attr("class"),
			dataName = "",
			id = $this.parent().siblings(".td-delete").find("button").data("expense-id")

		if (spanClass == "expected-cost") {
			dataName = "expected_cost"
			if (data == 0) {
				data = null
			}
		} else if (spanClass == "cost") {
			dataName = "cost"
		} else if (spanClass == "name") {
			dataName = "name"
		}

		$.ajax({
			url: `http://127.0.0.1:8000/api/expenses/${id}/`,
			type: "PATCH",
			headers: {
				"Content-Type": "application/json; charset=UTF-8",
				"X-CSRFToken": Cookies.get("csrftoken"),
				Accept: "application/json; charset=UTF-8",
			},
			data: JSON.stringify({ [dataName]: data }),
			success: function () {
				userCategoryTables();
				Toast.fire({
					icon: "success",
					title: `Saved changes!`,
				});
				userCategoryTables();
			},
			error: function (jqXHR, textStatus, errorThrown) {
				$this.html($this.data("before"))
				if (jqXHR.responseJSON) {
					let errorResponse = "";
					for (let [key, item] of Object.entries(jqXHR.responseJSON)) {
						if (Array.isArray(item)) {
							for (const error of item) {
								errorResponse += `${key}: ${error}<br>`;
							}
						} else {
							errorResponse += `${item}<br>`;
						}
					}
					Toast.fire({
						icon: "error",
						title: errorResponse,
					});
				} else {
					Toast.fire({
						icon: "error",
						title: "Error",
					});
				}
				console.log(textStatus, errorThrown);
				console.log(jqXHR);
			}
		});
	});
});