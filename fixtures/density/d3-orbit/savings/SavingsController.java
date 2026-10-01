public class SavingsController {
  public Page list(int p) { return svc.fetchPage(p); }
  // refs: orbit.savings.SavingsService#fetchPage shared.PageDto#of
}
