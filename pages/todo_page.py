from playwright.sync_api import Page, Locator


class TodoPage:
    def __init__(self, page: Page, base_url: str = "https://demo.playwright.dev/todomvc/#/"):
        self.page = page
        self.base_url = base_url

    def goto(self) -> None:
        self.page.goto(self.base_url)
        self.page.locator(".new-todo").wait_for(state="visible")

    @property
    def new_todo_input(self) -> Locator:
        return self.page.locator(".new-todo")

    @property
    def todo_list(self) -> Locator:
        return self.page.locator(".todo-list")

    @property
    def todo_items(self) -> Locator:
        return self.page.locator(".todo-list li")

    @property
    def todo_count_label(self) -> Locator:
        return self.page.locator(".todo-count")

    @property
    def filter_all(self) -> Locator:
        return self.page.get_by_role("link", name="All")

    @property
    def filter_active(self) -> Locator:
        return self.page.get_by_role("link", name="Active")

    @property
    def filter_completed(self) -> Locator:
        return self.page.get_by_role("link", name="Completed")

    @property
    def clear_completed_button(self) -> Locator:
        return self.page.locator(".clear-completed")

    @property
    def toggle_all_checkbox(self) -> Locator:
        return self.page.locator(".toggle-all")

    def add_todo(self, text: str) -> None:
        self.new_todo_input.fill(text)
        self.new_todo_input.press("Enter")

    def get_todo_by_index(self, index: int) -> Locator:
        return self.todo_items.nth(index)

    def get_todo_by_text(self, text: str) -> Locator:
        return self.todo_items.filter(has_text=text)

    def get_todo_toggle(self, index: int) -> Locator:
        return self.get_todo_by_index(index).locator(".toggle")

    def get_todo_destroy_button(self, index: int) -> Locator:
        return self.get_todo_by_index(index).locator(".destroy")

    def mark_complete(self, index: int) -> None:
        self.get_todo_toggle(index).check()

    def mark_incomplete(self, index: int) -> None:
        self.get_todo_toggle(index).uncheck()

    def delete_todo(self, index: int) -> None:
        todo = self.get_todo_by_index(index)
        todo.hover()
        self.get_todo_destroy_button(index).click()

    def mark_all_complete(self) -> None:
        self.toggle_all_checkbox.check()

    def clear_completed(self) -> None:
        self.clear_completed_button.click()

    def filter_by_all(self) -> None:
        self.filter_all.click()

    def filter_by_active(self) -> None:
        self.filter_active.click()

    def filter_by_completed(self) -> None:
        self.filter_completed.click()

    def get_todo_count(self) -> int:
        return self.todo_items.count()

    def get_remaining_count(self) -> int:
        return int(self.todo_count_label.inner_text().split()[0])

    def get_visible_todo_texts(self) -> list[str]:
        return [
            self.get_todo_by_index(i).locator("label").inner_text()
            for i in range(self.get_todo_count())
        ]

    def is_todo_completed(self, index: int) -> bool:
        return "completed" in (self.get_todo_by_index(index).get_attribute("class") or "")

    def todo_exists(self, text: str) -> bool:
        return self.get_todo_by_text(text).count() > 0
