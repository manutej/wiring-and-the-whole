public class AccountsController {
  public Page list(int p) { return svc.fetchPage(p); }
  // refs: orbit.accounts.AccountsService#fetchPage shared.PageDto#of
}
