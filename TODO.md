Task: Improve search performance in FileSystemModel and API

Steps:
1. ✅ Refactor FileSystemModel.search() to:
   - ✅ Use database indexed search on FileMetadata model for faster queries.
   - ✅ Add pagination support (page, per_page).
   - ✅ Cache search results for repeated queries.

2. ✅ Update api_controller.py search endpoint to:
   - ✅ Accept pagination parameters (page, per_page).
   - ✅ Return paginated search results with metadata (total, pages, current page).

3. ✅ Add error handling and logging for new parameters.

4. ✅ Test search performance and correctness.

5. ✅ Document changes in code comments.

Next steps:
- ✅ All tasks completed successfully
- ✅ Testing completed and verified working
