public class AccountsService {
  public Page fetchPage(int p) { return repo.findPage(p); }
  // refs: orbit.accounts.AccountsRepository#findPage
}
