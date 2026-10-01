public class AccountsService {
  public Page fetchPage(int p) { return repo.findPage(p); }
  // refs: fork.AccountsRepository#findPage
}
