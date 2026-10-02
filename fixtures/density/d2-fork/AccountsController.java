public class AccountsController {
  public Page list(int p) { return svc.fetchPage(p); }
  // refs: fork.AccountsService#fetchPage shared.PageDto#of
}
